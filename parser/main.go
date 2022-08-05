package main

import (
	"net/http"
	"os"
	"os/signal"
	"reflect"
	"syscall"

	"github.com/faceit/go-steam"
	"github.com/faceit/go-steam/netutil"
	"github.com/paralin/go-dota2"
	"github.com/paralin/go-dota2/events"
	"github.com/sirupsen/logrus"
)

func main() {
	lg := logrus.New()
	dc, readyCh := startDotaClient(lg)
	// Wait for client welcome then start server
	<-readyCh
	h := Handler{lg, dc}
	http.HandleFunc("/parse", h.handleParse)
	lg.Infoln("Starting HTTP server")
	http.ListenAndServe("0.0.0.0:5656", nil)

	// Wait for signal before closing
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
}

func startDotaClient(lg *logrus.Logger) (*dota2.Dota2, chan bool) {
	sc := steam.NewClient()
	dc := dota2.New(sc, lg)
	username, password := LoadSteamCredentials()
	auth := &steam.LogOnDetails{Username: username, Password: password}
	readyCh := make(chan bool)

	lg.Infoln("Connecting to server")
	sc.ConnectToBind(netutil.ParsePortAddr("103.10.124.162:27018"), nil)
	// Steam client message listener
	go func() {
		for evt := range sc.Events() {
			switch evt.(type) {
			case *steam.ConnectedEvent:
				lg.Infoln("Connected, logging in")
				sc.Auth.LogOn(auth)
			case *steam.ClientCMListEvent:
				lg.Infoln("Received server list")
			case *steam.LoggedOnEvent:
				lg.Infoln("Logged in, setting game played")
				sc.GC.SetGamesPlayed(dota2.AppID)
			case *steam.WebSessionIdEvent:
				lg.Infoln("Got a web session, saying hello")
				dc.SayHello()
			case *events.ClientWelcomed:
				lg.Infoln("Client welcomed!")
				readyCh <- true
			case *steam.PersonaStateEvent, *steam.AccountInfoEvent, *steam.LoginKeyEvent,
				*steam.FriendsListEvent, *events.GCConnectionStatusChanged,
				*events.ClientStateChanged:
			default:
				lg.Infoln(reflect.TypeOf(evt))
				lg.Infoln(evt)
			}
		}
	}()

	return dc, readyCh
}

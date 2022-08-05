package main

import (
	"compress/bzip2"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"

	"github.com/joeggg/mango"
	"github.com/paralin/go-dota2"
	"github.com/sirupsen/logrus"
)

type Handler struct {
	lg *logrus.Logger
	dc *dota2.Dota2
}

func (h *Handler) handleParse(rw http.ResponseWriter, req *http.Request) {
	qVals := req.URL.Query()
	matchId := qVals["match_id"][0]
	num, err := strconv.Atoi(matchId)
	if err != nil {
		rw.WriteHeader(http.StatusBadRequest)
		return
	}
	go processReplay(h.lg, h.dc, uint64(num))
}

func processReplay(lg *logrus.Logger, dc *dota2.Dota2, matchId uint64) {
	fname, err := downloadReplay(lg, dc, matchId)
	if err != nil {
		panic(err)
	}
	lg.Infof("Parsing replay %s\n", fname)
	rp := mango.WithDefaultGatherers(mango.NewReplayParser())
	err = rp.Initialise(fname)
	if err != nil {
		panic(err)
	}
	_, err = rp.ParseReplay()
	if err != nil {
		panic(err)
	}
	jsonStr, _ := json.MarshalIndent(rp.GetResults()["Chat"], "", "  ")
	fmt.Println(string(jsonStr))
}

func downloadReplay(lg *logrus.Logger, dc *dota2.Dota2, matchId uint64) (string, error) {
	ctx := context.Background()
	lg.Infof("Requesting match details for %d\n", matchId)
	matchResp, err := dc.RequestMatchDetails(ctx, matchId)
	if err != nil {
		return "", err
	}
	match := matchResp.GetMatch()
	url := fmt.Sprintf(
		"http://replay%d.valve.net/%d/%d_%d.dem.bz2",
		match.GetCluster(),
		dota2.AppID,
		matchId,
		match.GetReplaySalt(),
	)
	// Download, uncompress and save replay file
	lg.Infof("Downloading replay for %d\n", matchId)
	replayResp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	decomp := bzip2.NewReader(replayResp.Body)
	data, err := ioutil.ReadAll(decomp)
	if err != nil {
		return "", err
	}
	fname := fmt.Sprintf("%d.dem", matchId)
	os.WriteFile(fname, data, 0666)
	lg.Infof("Finished downloading replay for %d\n", matchId)
	return fname, err
}

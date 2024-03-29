package main

import (
	"compress/bzip2"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"

	"github.com/go-redis/redis/v9"
	"github.com/joeggg/mango"
	"github.com/paralin/go-dota2"
	"github.com/sirupsen/logrus"
)

const workQueue = "parser:work"
const resultKeyPrefix = "parser:result:"
const resultExpiry = time.Hour

type Worker struct {
	ctx context.Context
	r   *redis.Client
	lg  *logrus.Logger
	dc  *dota2.Dota2
}

func newWorker(lg *logrus.Logger, dc *dota2.Dota2) *Worker {
	ctx := context.Background()
	r := redis.NewClient(&redis.Options{Addr: "redis:6379", Password: "", DB: 0})
	return &Worker{ctx, r, lg, dc}
}

func (w *Worker) listen() {
	for {
		time.Sleep(time.Millisecond)
		work := w.r.LPop(w.ctx, workQueue)
		if err := work.Err(); err != nil {
			continue
		}
		matchId, err := work.Uint64()
		if err != nil {
			continue
		}
		go w.processReplay(matchId)
	}
}

func (w *Worker) processReplay(matchId uint64) {
	key := fmt.Sprintf("%s%d", resultKeyPrefix, matchId)
	fname, err := w.downloadReplay(matchId)
	if err != nil {
		w.handleFailure(key, err)
	}
	defer os.Remove(fname)

	w.lg.Infof("Parsing replay %s\n", fname)
	rp := mango.WithDefaultGatherers(mango.NewReplayParser())
	err = rp.Initialise(fname)
	if err != nil {
		w.handleFailure(key, err)
	}
	_, err = rp.ParseReplay()
	if err != nil {
		w.handleFailure(key, err)
	}
	jsonStr, _ := json.MarshalIndent(rp.GetResults(), "", "  ")
	w.lg.Infof("Finished parsing %s\n", fname)

	err = w.r.Set(w.ctx, key, string(jsonStr), resultExpiry).Err()
	if err != nil {
		w.handleFailure(key, err)
	}
}

func (w *Worker) handleFailure(key string, err error) {
	w.lg.Errorln(err)
	w.r.Del(w.ctx, key)
}

func (w *Worker) downloadReplay(matchId uint64) (string, error) {
	w.lg.Infof("Requesting match details for %d\n", matchId)
	matchResp, err := w.dc.RequestMatchDetails(w.ctx, matchId)
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
	w.lg.Infof("Downloading replay for %d\n", matchId)
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
	w.lg.Infof("Finished downloading replay for %d\n", matchId)
	return fname, err
}

package main

import (
	"os"
	"strings"
)

func LoadSteamCredentials() (string, string) {
	data, err := os.ReadFile("secret/steam_credentials.txt")
	if err != nil {
		panic(err)
	}
	creds := strings.Split(string(data), "\n")
	return creds[0], creds[1]
}

// goclient: a stock golang.org/x/crypto/ssh client with library-default algorithms.
// It completes key exchange against the target and exits; the delivered algorithm is read
// from the server's log by the oracle (as in Han, arXiv 2609.07849 §6), so authentication
// failure after KEX is expected and irrelevant.
package main

import (
	"fmt"
	"os"
	"time"

	"golang.org/x/crypto/ssh"
)

func main() {
	addr := os.Args[1]
	cfg := &ssh.ClientConfig{
		User:            "probe",
		Auth:            []ssh.AuthMethod{ssh.Password("x")},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Timeout:         5 * time.Second,
	}
	if len(os.Args) > 2 && os.Args[2] == "-Q" { // print the client's default KEX offer
		var c ssh.Config
		c.SetDefaults()
		fmt.Println(c.KeyExchanges)
		return
	}
	_, err := ssh.Dial("tcp", addr, cfg)
	fmt.Println("dial:", err)
}

package netclient

import (
	"crypto/tls"
	"fmt"
	"net"
)

type Client struct {
	Conn     net.Conn
	Incoming chan string
	Outgoing chan string
	System   chan string
	Errors   chan error
}

// NewClient initializes channels but does NOT connect
func NewClient() *Client {
	return &Client{
		Incoming: make(chan string),
		Outgoing: make(chan string),
		System:   make(chan string),
		Errors:   make(chan error),
	}
}

// Connect establishes TLS connection to the server
func (c *Client) Connect(addr string) error {
	config := &tls.Config{
		InsecureSkipVerify: true, // TEMP — matches your Python setup
	}

	conn, err := tls.Dial("tcp", addr, config)
	if err != nil {
		return err
	}

	c.Conn = conn
	c.System <- "Connected securely to server"
	return nil
}

// Authenticate sends username:password
func (c *Client) Authenticate(username, password string) error {
	payload := fmt.Sprintf("%s:%s\n", username, password)
	_, err := c.Conn.Write([]byte(payload))
	return err
}

// Start begins read/write goroutines
func (c *Client) Start() {
	go c.readLoop()
	go c.writeLoop()
}

// readLoop blocks forever reading server messages
func (c *Client) readLoop() {
	buf := make([]byte, 4096)

	for {
		n, err := c.Conn.Read(buf)
		if err != nil {
			c.Errors <- err
			return
		}

		msg := string(buf[:n])
		c.Incoming <- msg
	}
}

// writeLoop sends user messages to server
func (c *Client) writeLoop() {
	for msg := range c.Outgoing {
		_, err := c.Conn.Write([]byte(msg + "\n"))
		if err != nil {
			c.Errors <- err
			return
		}
	}
}

// Close cleanly shuts down the connection
func (c *Client) Close() {
	if c.Conn != nil {
		c.Conn.Close()
	}
	close(c.Incoming)
	close(c.Outgoing)
	close(c.System)
	close(c.Errors)
}
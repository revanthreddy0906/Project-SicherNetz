package main

import (
	"fmt"
	"os"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"securecomm-go-client/netclient"
)

/* ---------- App State ---------- */

type appState int

const (
	stateLogin appState = iota
	stateChat
)

/* ---------- Styles ---------- */

var (
	leftText    = lipgloss.NewStyle().Foreground(lipgloss.Color("252"))
	rightText   = lipgloss.NewStyle().Foreground(lipgloss.Color("42"))
	leftHeader  = lipgloss.NewStyle().Foreground(lipgloss.Color("39")).Bold(true)
	rightHeader = lipgloss.NewStyle().Foreground(lipgloss.Color("42")).Bold(true)

	systemStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("39")).
		Italic(true)

	inputStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("205"))

	errorStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("196")).
		Bold(true)
)

/* ---------- Tea Messages ---------- */

type serverMsg string
type systemMsg string
type errorMsg error

/* ---------- Chat Message ---------- */

type chatMessage struct {
	author string
	text   string
	self   bool
	sys    bool
}

/* ---------- Model ---------- */

type model struct {
	state appState

	// login
	username   string
	password   string
	focus      int
	authErr    string
	connecting bool

	// chat
	messages []chatMessage
	input    string
	width    int
	height   int

	client *netclient.Client
}

/* ---------- Init ---------- */

func initialModel() model {
	return model{state: stateLogin}
}

func (m model) Init() tea.Cmd {
	return nil
}

/* ---------- Protocol Parser ---------- */

func parseServerMessage(raw string) (chatMessage, bool) {

	// AUTH OK
	if strings.HasPrefix(raw, "OK:") {
		group := strings.TrimPrefix(raw, "OK:")
		return chatMessage{
			text: "Joined group " + group,
			sys:  true,
		}, true
	}

	// SYSTEM MESSAGE
	if strings.HasPrefix(raw, "[SYSTEM]") {
		return chatMessage{
			text: strings.TrimPrefix(raw, "[SYSTEM] "),
			sys:  true,
		}, true
	}

	// CHAT MESSAGE: [group] user: message
	if strings.HasPrefix(raw, "[") && strings.Contains(raw, "]") && strings.Contains(raw, ":") {
		parts := strings.SplitN(raw, "]", 2)
		body := strings.TrimSpace(parts[1])
		sub := strings.SplitN(body, ":", 2)

		if len(sub) == 2 {
			return chatMessage{
				author: strings.TrimSpace(sub[0]),
				text:   strings.TrimSpace(sub[1]),
			}, true
		}
	}

	return chatMessage{}, false
}

/* ---------- Commands ---------- */

func connectAndAuthCmd(c *netclient.Client, user, pass string) tea.Cmd {
	return func() tea.Msg {
		addr := os.Getenv("SC_SERVER_ADDR")
		if addr == "" {
			return errorMsg(fmt.Errorf("SC_SERVER_ADDR not set"))
		}

		if err := c.Connect(addr); err != nil {
			return errorMsg(err)
		}

		if err := c.Authenticate(user, pass); err != nil {
			return errorMsg(err)
		}

		c.Start()
		return systemMsg("AUTH_OK")
	}
}

func listenCmd(c *netclient.Client) tea.Cmd {
	return func() tea.Msg {
		select {
		case msg := <-c.Incoming:
			return serverMsg(msg)
		case msg := <-c.System:
			return systemMsg(msg)
		case err := <-c.Errors:
			return errorMsg(err)
		}
	}
}

/* ---------- Update ---------- */

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {

	/* ---------- LOGIN ---------- */
	if m.state == stateLogin {

		switch msg := msg.(type) {

		case tea.KeyMsg:
			switch msg.Type {

			case tea.KeyCtrlC, tea.KeyEsc:
				return m, tea.Quit

			case tea.KeyTab:
				m.focus = (m.focus + 1) % 2

			case tea.KeyBackspace:
				if m.focus == 0 && len(m.username) > 0 {
					m.username = m.username[:len(m.username)-1]
				}
				if m.focus == 1 && len(m.password) > 0 {
					m.password = m.password[:len(m.password)-1]
				}

			case tea.KeyRunes:
				if m.focus == 0 {
					m.username += string(msg.Runes)
				} else {
					m.password += string(msg.Runes)
				}

			case tea.KeyEnter:
				if m.username == "" || m.password == "" {
					m.authErr = "Username and password required"
					return m, nil
				}

				m.connecting = true
				m.authErr = ""
				m.client = netclient.NewClient()

				return m, tea.Batch(
					connectAndAuthCmd(m.client, m.username, m.password),
					listenCmd(m.client),
				)
			}

		case systemMsg:
			if string(msg) == "AUTH_OK" {
				m.state = stateChat
				m.connecting = false
				m.messages = []chatMessage{
					{text: "You joined the group", sys: true},
				}
				return m, listenCmd(m.client)
			}

		case errorMsg:
			m.connecting = false
			m.authErr = msg.Error()
			m.client = nil
		}

		return m, nil
	}

	/* ---------- CHAT ---------- */

	switch msg := msg.(type) {

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case serverMsg:
		if parsed, ok := parseServerMessage(string(msg)); ok {

			// mark self messages
			if parsed.author == m.username {
				parsed.self = true
			}

			m.messages = append(m.messages, parsed)
		}
		return m, listenCmd(m.client)

	case systemMsg:
		m.messages = append(m.messages, chatMessage{
			text: string(msg),
			sys:  true,
		})
		return m, listenCmd(m.client)

	case errorMsg:
		m.messages = append(m.messages, chatMessage{
			text: "Connection error: " + msg.Error(),
			sys:  true,
		})
		return m, nil

	case tea.KeyMsg:
		switch msg.Type {

		case tea.KeyCtrlC, tea.KeyEsc:
			return m, tea.Quit

		case tea.KeyEnter:
			clean := strings.TrimSpace(m.input)
			if clean != "" && m.client != nil {
				m.messages = append(m.messages, chatMessage{
					author: m.username,
					text:   clean,
					self:   true,
				})
				m.client.Outgoing <- clean
				m.input = ""
			}

		case tea.KeyBackspace:
			if len(m.input) > 0 {
				m.input = m.input[:len(m.input)-1]
			}

		case tea.KeySpace:
			m.input += " "

		case tea.KeyRunes:
			m.input += string(msg.Runes)
		}
	}

	return m, nil
}

/* ---------- Views ---------- */

func (m model) View() string {
	if m.state == stateLogin {
		return m.loginView()
	}
	return m.chatView()
}

func (m model) loginView() string {
	var b strings.Builder

	b.WriteString("\n🔐 Secure Login\n\n")

	if m.connecting {
		b.WriteString(systemStyle.Render("● Connecting & authenticating…\n\n"))
	}

	if m.authErr != "" {
		b.WriteString(errorStyle.Render("✗ " + m.authErr))
		b.WriteString("\n\n")
	}

	userStyle := lipgloss.NewStyle()
	passStyle := lipgloss.NewStyle()

	if m.focus == 0 {
		userStyle = userStyle.Underline(true)
	} else {
		passStyle = passStyle.Underline(true)
	}

	b.WriteString("Username:\n")
	b.WriteString(userStyle.Render("> " + m.username))
	b.WriteString("\n\n")

	b.WriteString("Password:\n")
	b.WriteString(passStyle.Render("> " + strings.Repeat("•", len(m.password))))
	b.WriteString("\n\n")

	b.WriteString(
		lipgloss.NewStyle().
			Foreground(lipgloss.Color("240")).
			Render("Tab → switch | Enter → login | Ctrl+C → quit"),
	)

	return b.String()
}

func (m model) chatView() string {
	var chat strings.Builder

	maxWidth := m.width - 6
	if maxWidth < 20 {
		maxWidth = 20
	}

	var lastAuthor string

	for _, msg := range m.messages {

		if msg.sys {
			chat.WriteString(systemStyle.Render("• "+msg.text) + "\n\n")
			lastAuthor = ""
			continue
		}

		if msg.author != lastAuthor {
			header := "[" + msg.author + "]"
			if msg.self {
				chat.WriteString(lipgloss.PlaceHorizontal(maxWidth, lipgloss.Right, rightHeader.Render(header)) + "\n")
			} else {
				chat.WriteString(leftHeader.Render(header) + "\n")
			}
		}

		if msg.self {
			chat.WriteString(lipgloss.PlaceHorizontal(maxWidth, lipgloss.Right, rightText.Render(msg.text)) + "\n\n")
		} else {
			chat.WriteString(leftText.Render(msg.text) + "\n\n")
		}

		lastAuthor = msg.author
	}

	chat.WriteString(inputStyle.Render("> " + m.input))
	return chat.String()
}

/* ---------- Main ---------- */

func main() {
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if err := p.Start(); err != nil {
		fmt.Println("Error:", err)
	}
}
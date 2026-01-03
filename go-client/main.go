package main

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

/* ---------- Styles ---------- */

var (
	leftText = lipgloss.NewStyle().
		Foreground(lipgloss.Color("252"))

	rightText = lipgloss.NewStyle().
		Foreground(lipgloss.Color("42"))

	leftHeader = lipgloss.NewStyle().
		Foreground(lipgloss.Color("39")).
		Bold(true)

	rightHeader = lipgloss.NewStyle().
		Foreground(lipgloss.Color("42")).
		Bold(true)

	systemStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("39")).
		Italic(true)

	inputStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("205"))
)

/* ---------- Message Model ---------- */

type chatMessage struct {
	author string
	text   string
	self   bool
	sys    bool
}

/* ---------- App Model ---------- */

type model struct {
	username string
	messages []chatMessage
	input    string
	width    int
	height   int
}

/* ---------- Init ---------- */

func initialModel() model {
	return model{
		username: "You",
		messages: []chatMessage{
			{sys: true, text: "You joined the group"},
		},
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

/* ---------- Update ---------- */

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {

	switch msg := msg.(type) {

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case tea.KeyMsg:
		switch msg.Type {

		case tea.KeyCtrlC, tea.KeyEsc:
			m.messages = append(m.messages, chatMessage{
				sys:  true,
				text: m.username + " left the group",
			})
			return m, tea.Quit

		case tea.KeyEnter:
			clean := strings.TrimSpace(m.input)
			if clean != "" {
				m.messages = append(m.messages, chatMessage{
					author: m.username,
					text:   clean,
					self:   true,
				})
			}
			m.input = ""

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

/* ---------- View ---------- */

func (m model) View() string {
	var chat strings.Builder

	maxWidth := m.width - 6
	if maxWidth < 20 {
		maxWidth = 20
	}

	var lastAuthor string

	for _, msg := range m.messages {

		// SYSTEM MESSAGE
		if msg.sys {
			chat.WriteString(
				systemStyle.
					Width(maxWidth).
					Render("• "+msg.text) + "\n\n",
			)
			lastAuthor = ""
			continue
		}

		// AUTHOR HEADER (only if author changed)
		if msg.author != lastAuthor {
			header := "[" + msg.author + "]"

			if msg.self {
				chat.WriteString(
					lipgloss.PlaceHorizontal(
						maxWidth,
						lipgloss.Right,
						rightHeader.Render(header),
					) + "\n",
				)
			} else {
				chat.WriteString(
					leftHeader.Render(header) + "\n",
				)
			}
		}

		// MESSAGE BODY
		if msg.self {
			chat.WriteString(
				lipgloss.PlaceHorizontal(
					maxWidth,
					lipgloss.Right,
					rightText.Render(msg.text),
				) + "\n\n",
			)
		} else {
			chat.WriteString(
				leftText.Render(msg.text) + "\n\n",
			)
		}

		lastAuthor = msg.author
	}

	chat.WriteString("\n")
    chat.WriteString(inputStyle.Render("> "))
    chat.WriteString(m.input)
	return chat.String()
}

/* ---------- Main ---------- */

func main() {
	p := tea.NewProgram(
		initialModel(),
		tea.WithAltScreen(),
	)

	if err := p.Start(); err != nil {
		fmt.Println("Error:", err)
	}
}
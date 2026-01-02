package main

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

/* ---------- Styles ---------- */

var (
	leftStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("252")).
		Align(lipgloss.Left)

	rightStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("42")).
		Align(lipgloss.Right)

	systemStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("240")).
		Italic(true)

	inputStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("205"))
)

/* ---------- Model ---------- */

type chatMessage struct {
	author string
	text string
	self bool
	sys  bool
}

type model struct {
	messages []chatMessage
	input    string
	width    int
	height   int
}

/* ---------- Init ---------- */

func initialModel() model {
	return model{
		messages: []chatMessage{
			{text: "user2 joined the chat", sys: true},
			{text: "Hey! This UI looks clean 👀", self: false},
			{text: "Yeah, much better than before!", self: true},
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
			return m, tea.Quit

		case tea.KeyEnter:
			if strings.TrimSpace(m.input) != "" {
				m.messages = append(m.messages, chatMessage{
					author: "You",
					text:   m.input,
					self:   true,
				})
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
/* ---------- View ---------- */
func (m model) View() string {
	var chat strings.Builder
	maxWidth := m.width - 4

	for _, msg := range m.messages {

		content := fmt.Sprintf("[%s]\n%s", msg.author, msg.text)

		if msg.self {
			chat.WriteString(
				rightStyle.
					Width(maxWidth).
					Render(content) + "\n\n",
			)
		} else {
			chat.WriteString(
				leftStyle.
					Width(maxWidth).
					Render(content) + "\n\n",
			)
		}
	}

	chat.WriteString("\n")
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

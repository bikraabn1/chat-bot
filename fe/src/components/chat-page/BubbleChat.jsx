import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Card } from 'antd'

const BubbleChat = ({ text, left }) => {
    const TextMarkdown = ({ children }) => <p style={{ color: "#ffffff" }}>{children}</p>
    const List = ({ children }) => <li style={{ color: "#ffffff" }}>{children}</li>
    const Header4 = ({ children }) => <h4 style={{ color: "#ffffff" }}>{children}</h4>
    const HorizontalRule = () => <hr style={{ color: "#ffffff" }} />
    const OrderedList = ({ children }) => <ol style={{ marginBlock: 12, marginLeft: 32 }}>{children}</ol>
    const UnorederedList = ({ children }) => <ul style={{ marginBlock: 12, marginLeft: 32 }}>{children}</ul>

    return (
        <Card size='small' style={{ maxWidth: 700, background: '#1677FF', alignSelf: left ? 'flex-end' : 'flex-start' }}>
            <ReactMarkdown
                components={{
                    p: TextMarkdown,
                    li: List,
                    h4: Header4,
                    hr: HorizontalRule,
                    ol: OrderedList,
                    ul: UnorederedList
                }}>
                {text}
            </ReactMarkdown>
        </Card>
    )
}

export default BubbleChat
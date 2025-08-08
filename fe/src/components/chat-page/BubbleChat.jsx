import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Card } from 'antd'

const BubbleChat = ({ text, left }) => {
    const textMarkdown = ({ children }) => <p style={{color: "#ffffff"}}>{children}</p>
    const Li = ({ children }) => <li style={{color: "#ffffff"}}>{children}</li>
    const H4 = ({ children }) => <h4 style={{color: "#ffffff"}}>{children}</h4>
    const Hr = () => <hr style={{color: "#ffffff"}} />
    const ol = ({children}) => <ol style={{marginBlock: 12, marginLeft: 32}}>{children}</ol>
    const ul = ({children}) => <ul style={{marginBlock: 12, marginLeft: 32}}>{children}</ul>

    return (
        <Card size='small' style={{ maxWidth: 700, background: '#1677FF', alignSelf: left ? 'flex-end' : 'flex-start' }}>
            <ReactMarkdown components={{p : textMarkdown, li: Li, h4: H4, hr: Hr, ol: ol, ul: ul}}>{text}</ReactMarkdown>
        </Card>
    )
}

export default BubbleChat
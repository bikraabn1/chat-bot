import React from 'react'
import { Flex, Typography } from 'antd'
import BubbleChat from './BubbleChat'

const ChatCanvas = ({ history }) => {
    const { Title } = Typography
    return (
        <div style={{ flex: 1, overflow: "scroll", marginBottom: 24 }}>
            <Flex vertical gap={5}>
                {history ?
                    history.map((item, index) => {
                        return(
                            <BubbleChat key={index} text={item.text} left={item.isMine}/>
                        )
                    }) :
                    (
                        <Title level={4} style={{width: '100%', textAlign: 'center'}}>Start a Message !!</Title>
                    )
                }
            </Flex>
        </div>
    )
}

export default ChatCanvas


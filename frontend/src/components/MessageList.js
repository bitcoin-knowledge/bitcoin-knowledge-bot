import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Styled from 'styled-components';
import ReactLoading from 'react-loading';
import {FaRobot, FaUserAlt} from 'react-icons/fa'
import { v4 as uuidv4 } from 'uuid';
import './Chatbot.css'

const MessageList = ({messages, bottomListRef, loading, collapsed}) => {
    const scrollComponentStyles = {
        marginRight: '10%',
    }

    return (
        <InfiniteScroll
          dataLength={messages.length} //This is important field to render the next data
          loader={<h4>Loading...</h4>}
          height={collapsed ? 500 : 300}
          style={scrollComponentStyles}
        >
          <MessageListContainer>
            {messages.map((message) => {
              return(
                <li key={uuidv4()} className={message.name === "User" ? "chat-message-user" : "chat-message"}>
                  {message.name === "User" ?
                  <ChatImage>
                    <FaUserAlt style={{fontSize: '1rem', marginTop: '3%'}} />
                    <ChatUser>{message.name}</ChatUser>
                  </ChatImage>
                  :
                  <ChatImage>
                    <FaRobot style={{fontSize: '1.2rem'}} />
                    <ChatUser>{message.name}</ChatUser>
                  </ChatImage>
                  }
                  <ChatMessage>{message.text}</ChatMessage>
                </li>
              )
            })}
          </MessageListContainer>
          <ChatBubbles>
              {loading === true ? <ReactLoading type={'bubbles'} color={'#f2a900'} height={'7%'} width={'7%'} /> : null}
          </ChatBubbles>
          <div ref={bottomListRef} />
        </InfiniteScroll>
    )
}

export default MessageList;

const MessageListContainer = Styled.ul`
    list-style-type: none;
    width: 80%;
    margin: 1% auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    color: white;
    padding-left: 10%;
    padding-right: 5%;
`;

const ChatBubbles = Styled.div`
    display: flex;
    padding-left: 13%;
`;

const ChatMessage = Styled.div`
    margin-top: 4%;
    padding-bottom: 2%;
    margin-bottom: 0;
    text-align: start;
`;

const ChatUser = Styled.div`
    margin-bottom: 0%;
    text-align: start;
    margin-left: 10px;
`;

const ChatImage = Styled.div`
    width: 60%;
    margin-left: 0;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    margin-top: 0.5%;
    margin-bottom: 0%;
    text-align: start;
`;
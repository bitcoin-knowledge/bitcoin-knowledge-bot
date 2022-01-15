import React, {useEffect, useState, useRef} from 'react';
import Styled from 'styled-components'
import MessageList from './MessageList';
import media from '../utils/ComponentBreakpoints'
import axios from 'axios'
import ArticleSuggestion from './ArticleSuggestion';
import './Chatbot.css'

const Chatbot = () => {
  const inputRef = useRef();
  const bottomListRef = useRef()
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [id, setId] = useState(4)
  const [collapsed, setCollapsed] = useState(false);
  const [articles, setArticles] = useState([])
  const [messages, setMessages] = useState([
    {
        id: 1,
        text: 'Hello World!',
        name: "Bot"
    },
    {
        id: 2,
        text: "I'm Bitcoin Knowledge Bot",
        name: "Bot"
    },
    {
        id: 3,
        text: "What can I answer for you?",
        name: "Bot"
    }
  ])

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [inputRef]);

  const formatChatLog = () => {
    let chatLog = ''
    messages.map(message => {
      // Skip over the bot greeting
      if (message.id > 3) {
        chatLog += `${message.name}: ${message.text}\n\n###\n\n`
      }
      return null
    })
    return chatLog
  }

  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage && lastMessage.name === 'User') {
      setLoading(true)
      const log = formatChatLog()
      axios.post("http://bitcoin-knowledge-bot.herokuapp.com/ask", {chat_log: log})
      .then(response => {
        setTimeout(() => {
          setId(id + 1)
          setArticles(response.data.articles)
          setMessages([...messages, {
            id: id,
            text: response.data.answer,
            name: "Bot"
          }])
          setLoading(false)
          // Scroll down to the bottom of the list
          bottomListRef.current.scrollIntoView({ behavior: 'smooth' });
        }, 3000)
      })
      .catch(error => {
          console.log(error)
      })
    }
  }, [messages])

  const handleOnSubmit = e => {
    e.preventDefault();
    // create user message from prompt
    setId(id + 1)
    const userMessage = {
      id: id,
      text: newMessage,
      name: "User"
    }
    // add user message to messages
    setTimeout(() => {
      setMessages([...messages, userMessage])
      // Scroll down to the bottom of the list
      bottomListRef.current.scrollIntoView({ behavior: 'smooth' });
    }, 1000)
    // Clear input field
    setNewMessage('');
  }

  const handleOnChange = e => {
    setNewMessage(e.target.value);
  };

  return (
    <div>
    <ChatWindow>
      <MessageList collapsed={collapsed} messages={messages} bottomListRef={bottomListRef} loading={loading} />
      <ChatForm
        onSubmit={handleOnSubmit}
        disabled={!newMessage}
        >
        <ChatButtonContainer>
          <ChatInput 
            type='text'
            value={newMessage}
            onChange={handleOnChange}
            placeholder="Type your message here..."
            ref={inputRef}
            />
          <ChatButton>send</ChatButton>
        </ChatButtonContainer>
      </ChatForm>
    </ChatWindow>
    <ArticleSuggestion articles={articles} setCollapsed={setCollapsed} collapsed={collapsed} loading={loading} />
    </div>
  )
}

export default Chatbot;

const ChatWindow = Styled.div`
    width: 80%;
    margin: 0% auto;
    margin-top: 0.5%;
    border: 4px solid #F2A900;
    border-top: 45px solid #F2A900;
    border-radius: 25px;
    background: #4F6272;
    padding: 0.5%;
    padding-left: 0%;
    padding-right: 0%;
    ${media.phone`
        width: 100%;
        margin: 0% auto;
        border-radius: 0px;
    `}
    ${media.tablet`
        width: 100%;
        margin: 0% auto;
        border-radius: 0px;
    `}
`;

const ChatForm = Styled.form`
    width: 100%;
    margin: 0% auto;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    border-top: 4px solid #F2A900;
    border-radius: 35px;
    padding-top: 0.5%;
`;

const ChatInput = Styled.input`
    margin: 0% auto;
	  width: 85%;
	  padding: 0.5%;
    border: 1px solid white;
    border-radius: 10px;
`;

const ChatButtonContainer = Styled.section`
    width: 80%;
    margin: 0.2% auto;
    display: flex;
    flex-direction: row;
    ${media.tablet`
        width: 90%;
    `}
    ${media.laptop`
        width: 90%;
    `}
`;

const ChatButton = Styled.button`
    width: 8%;
    padding: 1%;
    cursor: pointer;
    transition: all .5s ease;
    color: #F2A900;
    border: 3px solid black;
    text-align: center;
    line-height: 1;
    font-size: 17px;
    background-color : transparent;
    outline: none;
    border-radius: 4px;
    &:hover {
      color: #001F3F;
      background-color: #F2A900;
    }
    ${media.phone`
        width: 20%;
        margin-left: 5%;
    `}
    ${media.tablet`
        width: 20%;
        margin-left: 5%;
    `}
    ${media.laptop`
        width: 20%;
        margin-left: 5%;
    `}
`;
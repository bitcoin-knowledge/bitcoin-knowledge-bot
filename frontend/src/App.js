import React, {useState, useEffect} from 'react';
import Styled from 'styled-components';
import media from './utils/ComponentBreakpoints'
import axios from 'axios';
import Chatbot from './components/Chatbot';
import './index.css';

function App() {
  const [botStatus, setBotStatus] = useState('Loading...');
  
  useEffect(() => {
    axios.get("https://bitcoin-knowledge-bot.herokuapp.com/")
    .then(response => {
        setBotStatus(response.data)
    })
    .catch(error => {
        console.log(error)
    })
},[]);
 
return (
    <AppContainer>
        <Header>
            <HeaderTitle>Bitcoin Knowledge Bot</HeaderTitle>
            Status:
            <span style={botStatus === 'Loading...' ? {color: "red", textDecoration: "underline"} : {color: "green", textDecoration: "underline"}}>{botStatus}</span>
            <HeaderBody>
                <p>A question & answer AI bot that also suggests articles/podcasts <br/> Powered by GPT-3 and trained on an open source dataset of established Bitcoin knowledge</p>
                <HeaderSection>
                    <div className="content__item">
                        <a href="https://github.com/bitcoin-knowledge/bitcoin-knowledge-bot" target="_blank" rel="noreferrer"><button className="button button--pandora"><span>code</span></button></a>
                    </div>
                    <div className="content__item">
                        <a href="https://github.com/bitcoin-knowledge/bitcoin-knowledge-bot/tree/main/datasets" target="_blank" rel="noreferrer"><button className="button button--pandora"><span>datasets</span></button></a>
                    </div>
                </HeaderSection>
            </HeaderBody>
        </Header>
        <Chatbot />
    </AppContainer>
    )
}

export default App;

const AppContainer = Styled.div`
    margin: 0% auto;
    text-align: center;
    overflow: false;
`;

const Header = Styled.header`
    width: 60%;
    margin: 0% auto;
    margin-bottom: 0%;
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 10px solid #F2A900;
    border-radius: 10px;
    padding-bottom: 0.5%;
    ${media.phone`
        width: 96%;
        margin: 1% auto;
        `}
    ${media.tablet`
        width: 96%;
        margin: 1% auto;
    `}
`;

const HeaderBody = Styled.div`
    width: 80%;
    margin: 1% auto;
    border-top: 2px solid #404E5C;
    margin-bottom: 0%;
`;

const HeaderSection = Styled.div`
    width: 70%;
    margin: 0% auto;
    display: flex;
    justify-content: space-around;
`;

const HeaderTitle = Styled.h1`
    margin-top: 0.5%;
    margin-bottom: 1%;
`;
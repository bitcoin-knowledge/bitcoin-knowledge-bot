import React, {useState} from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Styled from 'styled-components';
import media from "../utils/ComponentBreakpoints";
import ReactLoading from 'react-loading';
import {FaChevronDown, FaChevronUp} from 'react-icons/fa';
import { v4 as uuidv4 } from 'uuid';
import './Chatbot.css'

const ArticleSuggestion = ({loading, collapsed, setCollapsed}) => {
    const scrollComponentStyles = {
        paddingRight: '1%',
    }

    const articles = [
        {
            link: 'https://nakamotoinstitute.org/bitcoin/',
            title: 'Bitcoin: A Peer-to-Peer Electronic Cash System',
            text: "To compensate for increasing hardware speed and varying interest in running nodes over time, the proof-of-work difficulty is determined by a moving average targeting an average number of blocks per hour. If they're generated too fast, the difficulty increases."
        },
        {
            link: 'https://nakamotoinstitute.org/shelling-out/',
            title: 'Shelling out: The Origins of Money',
            text: "The precursors of money, along with language, enabled early modern humans to solve problems of cooperation that other animals cannot \u2013 including problems of reciprocal altruism, kin altruism, and the mitigation of aggression. These precursors shared with non-fiat currencies very specific characteristics \u2013 they were not merely symbolic or decorative objects."
        },
        {
            link: 'https://nakamotoinstitute.org/mempool/bitcoin-is-the-great-definancialization/',
            title: 'Bitcoin is the Great Definancialization',
            text: "Have you ever had a financial advisor (or maybe even a parent) tell you that you need to make your money grow? This idea has been so hardwired in the minds of hard-working people all over the world that it has become practically second nature to the very idea of work."
        }
    ]
    return (
        <ArticleContainer>
            <ArticleContainerHeader>
                <ArticleCollapse onClick={() => setCollapsed(!collapsed)}>
                    {collapsed ? <FaChevronUp /> : <FaChevronDown />}
                </ArticleCollapse>
                <ArticleSuggestionTitle>
                    article suggestion coming soon...
                </ArticleSuggestionTitle>
            </ArticleContainerHeader>
            {
                collapsed ? 
                <CollapsedContainer />
                :
                <InfiniteScroll
                dataLength={articles.length} //This is important field to render the next data
                loader={<h4>Loading...</h4>}
                height={window.innerWidth > 800 ? 230: 350}
                style={scrollComponentStyles}
                >
                {
                    loading 
                ?
                <ChatBubbles>
                    <ReactLoading type={'bubbles'} color={'#f2a900'} height={'10%'} width={'10%'} />
                </ChatBubbles>
                :
                articles.map((article) => {
                    return(
                        <Article key={uuidv4()}>
                        <ArticleTitle>{article.title}</ArticleTitle>
                        <ArticleText>"{article.text}"</ArticleText>
                        <ArticleAnchor href={article.link} target="_blank" rel="noreferrer">read</ArticleAnchor>
                    </Article>
                    )
                })
                }
            </InfiniteScroll>
            }
        </ArticleContainer>
    )
}

export default ArticleSuggestion;

const ArticleContainer = Styled.div`
    width: 78%;
    margin: 1% auto;
    border: 4px solid #F2A900;
    border-radius: 25px;
    background: #4F6272;
    ${media.tiny`
        width: 98%;
        margin: 0% auto;
        border-radius: 0px;
    `}
    ${media.phone`
        width: 98%;
        margin: 0% auto;
        border-radius: 0px;
    `}
    ${media.tablet`
        width: 98%;
        margin: 0% auto;
        border-radius: 0px;
    `}
`;

const ArticleContainerHeader = Styled.div`
    width: 100%;
    margin: 0% auto;
    margin-top: 0;
    background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
    display: flex;
    border-top: 5px solid #F2A900;
    border-left: 2px solid #F2A900;
    border-right: 2px solid #F2A900;
    border-bottom: 2px solid #F2A900;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
`;

const ArticleCollapse = Styled.div`
    cursor: pointer;
    padding: 0.3%;
    margin: 0.5%;
    border-radius: 50px;
    border: 1px solid transparent;
    &:hover {
        background-color: #57b8f0;
        border: 1px solid white;
    }
`;

const ArticleSuggestionTitle = Styled.h4`
    color: white;
    margin: 0 auto;
`;

const Article = Styled.div`
    display: flex;
    align-items: center;
    border: 2px solid white;
    border-radius: 10px;
    background-image: linear-gradient(135deg, #f2a900 0%, #FF6A88 86%, #FF99AC 100%);
    margin: 1% auto;
    margin-left: 1.5%;
`;

const ArticleTitle = Styled.h3`
    color: white;
    font-size: 1.2rem;
    padding: 0.5%;
    margin-top: 0;
    margin-bottom: 0;
    width: 20%;
    ${media.phone`
        font-size: 1rem;
    `}
    ${media.tablet`
        font-size: 1rem;
    `}
`;

const ArticleText = Styled.p`
    color: white;
    border-left: 2px solid white;
    border-right: 2px solid white;
    padding: 1%;
    width: 70%;
`;

const ArticleAnchor = Styled.a`
    width: 10%;
    text-decoration: none;
    margin: 1% auto;
    margin-left: 1%;
    margin-right: 1%;
    padding: 1%;
    cursor: pointer;
    transition: all .5s ease;
    color: white;
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
`;

const ChatBubbles = Styled.div`
    display: flex;
    justify-content: center;
`;

const CollapsedContainer = Styled.div`
    width: 78%;
    margin: 1% auto;
    background: #4F6272;
`;

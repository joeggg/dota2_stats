import * as React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import './App.css';
import Main from './main';
import Matches from './matches';
import Parse from './parse';
import Scoreboard from './scoreboard';

import logo from './dota2.svg';

function App(): React.ReactElement {
    return (
        <div className="App">
            <header className="App-header">
                <h3 className="title">
                    <img src={logo} className="App-logo" alt="logo" />
                    <a href="/" className='Title-Text'>
                        Joe&apos;s Dota Stats
                        <br />
                    </a>
                </h3>
            </header>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Main />} />
                    <Route path="players/:accountId" element={<Matches />} />
                    <Route
                        path="players/:accountId/match/:matchId"
                        element={<Scoreboard />}
                    />
                    <Route path="parse" element={<Parse />} />
                </Routes>
            </BrowserRouter>
            <footer></footer>
        </div>
    );
}

export default App;

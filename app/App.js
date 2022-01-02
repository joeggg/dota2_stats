import { BrowserRouter, Route, Routes } from 'react-router-dom';
import logo from './dota2.svg';
import './App.css';
import Main from './main';
import Matches from './matches';
import Scoreboard from './scoreboard';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h3 className="title">
                    <a href="/">
                        <img src={logo} className="App-logo" alt="logo" />
                        Joe&apos;s Dota Stats
                        <br />
                    </a>
                </h3>
            </header>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Main />} />
                    <Route path="players/:accountId" element={<Matches />}>
                        <Route path="match/:matchId" element={<Scoreboard />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;

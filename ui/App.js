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
                    {/* <Route path="match/:matchId/parse" element={<Parse />} /> */}
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;

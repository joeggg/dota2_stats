import { BrowserRouter, Route, Routes } from 'react-router-dom';
import MatchList from './match_list';
import logo from './dota2.svg';
import './App.css';
import Main from './main';

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
                    <Route path=":accountId" element={<MatchList />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;

import { useEffect, useState } from 'react';
import logo from './dota2.svg';
import './App.css';

function App() {

  const [match_data, setMatches] = useState([]);
  const account_id = 54269634;
  const ip = '94.11.9.194';

  useEffect(() => {
    fetch(`http://${ip}:5656/matches/${account_id}`).then(res => {
      res.text().then(stuff => {
        const matches = JSON.parse(stuff).results;
        const data = matches.map(match => {
          const time = new Date(1000*match.start_time)
          let isRadiant = null;
          for (const player of match.players) {
            if (player.account_id === account_id) {
              isRadiant = player.player_slot < 5;
              break;
            }
          }
          return (
            <h5 key={match.match_id}>
              {time.toISOString().substring(0, 16).replace('T', ' ')} | {match.match_id} | {isRadiant === match.radiant_win ? "won" : "lost"}
            </h5>
          );
        });
        setMatches((<div>{data}</div>))
        // console.log(matches);
      })
    })
  });

  return (
    <div className='App'>
      <header className='App-header'>
        <img src={logo} className='App-logo' alt='logo' />
        <p>
          Dota stuff goes here <br></br>
          Matches: 
        </p>
        {match_data}
        <a
          className='App-link'
          href='https://dota2.com'
          target='_blank'
          rel='noopener noreferrer'
        >
          Dota 2 site
        </a>
      </header>
    </div>
  );
}

export default App;

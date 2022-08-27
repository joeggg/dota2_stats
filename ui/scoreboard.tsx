import * as React from 'react'
import { Link, useParams } from 'react-router-dom';

import ParseResults from './parseResults';
import { heroIconURI, url } from './consts'
const heroNames = require('./hero_icon_names.json')


interface Match {
    players: any[],
    winner: string
}

function Scoreboard(): React.ReactElement {
    const params = useParams();
    const [matchData, setMatchData] = React.useState({} as Match);
    const [matchScoreboard, setMatchScoreboard] = React.useState(<div></div>);
    const [parseResults, setParseResults] = React.useState(<div></div>);

    const accountId: string = params.accountId!;
    const matchId: string = params.matchId!;

    /**
     *  Match scoreboard effect
     */
    React.useEffect(() => {
        fetch(`${url}/match/${matchId}?account_id=${accountId}`).then((res) => {
            res.text().then((text) => {
                const matchObj = JSON.parse(text);
                const match: Match = matchObj!.match;
                // const PlayerDetails = matchObj.player;
                // Create the scoreboard element
                const scoreboard = match.players.map((player: any) => {
                    const uri = heroNames[player.hero] ? heroIconURI.replace('*', heroNames[player.hero]) : '';
                    let colour: string;
                    let id = player.id;
                    if (player.slot === 5 || player.slot === 0) {
                        id = 'GapRow';
                    }
                    if (player.slot < 5) {
                        colour = 'darkgreen';
                    } else {
                        colour = 'darkred';
                    }
                    return (
                        <tr key={player.id}>
                            <td
                                className='ScoreRow Hero'
                                id={id}
                                style={{ color: colour }}
                            >
                                <img
                                    className='SHeroIcon'
                                    src={uri}
                                />
                            </td>
                            <td className='ScoreRow Level' id={id}>
                                {player.level}
                            </td>
                            <td className='ScoreRow Kills' id={id}>
                                {player.kills}
                            </td>
                            <td className='ScoreRow Deaths' id={id}>
                                {player.deaths}
                            </td>
                            <td className='ScoreRow Assists' id={id}>
                                {player.assists}
                            </td>
                            <td className='ScoreRow NetWorth' id={id}>
                                {player.net_worth}
                            </td>
                            <td className='ScoreRow GXpm' id={id}>
                                {`${player.gpm}/${player.xpm}`}
                            </td>
                            <td className='ScoreRow Dmg' id={id}>
                                {player.hero_damage}
                            </td>
                            <td className='ScoreRow TDmg' id={id}>
                                {player.tower_damage}
                            </td>
                            <td className='ScoreRow Healing' id={id}>
                                {player.healing}
                            </td>
                        </tr>
                    );
                });
                // Set the match scoreboard state and current display defaults to match list
                setMatchData(match);
                setMatchScoreboard(
                    <div>
                        <table cellSpacing={0} className='MatchData Centre' >
                            <thead>
                                <tr>
                                    <th className='ScoreHeader Hero'>Hero</th>
                                    <th className='ScoreHeader Level'>Level</th>
                                    <th className='ScoreHeader Kills'>Kills</th>
                                    <th className='ScoreHeader Deaths'>Deaths</th>
                                    <th className='ScoreHeader Assists'>Assists</th>
                                    <th className='ScoreHeader NetWorth'>Net worth</th>
                                    <th className='ScoreHeader GXpm'>GPM/XPM</th>
                                    <th className='ScoreHeader Dmg'>Hero damage</th>
                                    <th className='ScoreHeader TDmg'>Tower damage</th>
                                    <th className='ScoreHeader Healing'>Hero healing</th>
                                </tr>
                            </thead>
                            <tbody>{scoreboard}</tbody>
                        </table>
                    </div>
                );
            });
        });
    }, [matchId, accountId]);

    /**
     * Parser results
     */
    React.useEffect(() => {
        fetch(`${url}/match/${matchId}/parse`).then(res => res.json().then(data => {
            if (data.status === 'complete') {
                setParseResults(ParseResults(data.result))
            } else {
                setParseResults(<div><p className='MidText'>No parse results yet</p> </div >)
            }
        }));
    }, [matchId]);

    const onParse = () => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        };
        fetch(`${url}/match/${matchId}/parse`, requestOptions)
            .then(res => res.json());
    };

    return (
        <div className='Page'>
            <div className='ButtonContainer'>
                <button className='Button' id='Back'>
                    <Link to={`/players/${accountId}`}>
                        <p className='ButtonText'>Back to matches</p>
                    </Link>
                </button>
                <button className='Button' id='Parse' onClick={onParse}>
                    <Link to={`/parse?id=${matchId}`}>
                        <p className='ButtonText' >Parse replay</p>
                    </Link>
                </button>
            </div>
            <p className='MatchesTitle'>Match scoreboard</p>
            <p
                className='ResultsTitle'
                style={{
                    color: matchData.winner === 'Radiant' ? 'green' : 'darkred',
                }}
            >
                {matchData.winner} win!
            </p>
            {matchScoreboard}
            {parseResults}
        </div >
    );
}

export default Scoreboard;

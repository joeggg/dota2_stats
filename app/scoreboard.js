import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function Scoreboard() {
    const params = useParams();
    const [matchScoreboard, setMatchScoreboard] = useState(<div></div>);

    const matchId = params.matchId;
    const url = 'http://94.11.9.194:5656';
    // const ip = 'http://127.0.0.1:5656';

    /**
     *  Match scoreboard effect
     */
    useEffect(() => {
        fetch(`${url}/match/${matchId}`).then((res) => {
            res.text().then((text) => {
                const match = JSON.parse(text).results;
                // Create the scoreboard element
                const scoreboard = (
                    <table>Match scoreboard here for {match.matchId}</table>
                );
                // Set the match scoreboard state and current display defaults to match list
                setMatchScoreboard(
                    <div>
                        <button className="BackButton">Back to matches</button>
                        <table cellSpacing={0} className="MatchData">
                            Match scoreboard here {scoreboard}
                        </table>
                    </div>
                );
            });
        });
    }, []);

    return (
        <div className="Page">
            <p className="matches_title">
                Match scoreboard:
                <br />
            </p>
            {matchScoreboard}
        </div>
    );
}

export default Scoreboard;

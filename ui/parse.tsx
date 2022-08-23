import React from 'react';
import * as ReactRouterDOM from 'react-router-dom'
import { url } from './consts';


function Parse(): React.ReactElement {
    const [params,] = ReactRouterDOM.useSearchParams();
    const [display, setDisplay] = React.useState(<div></div>);
    const navigate = ReactRouterDOM.useNavigate();

    React.useEffect(() => {
        const matchId = params.get("id");
        let waitCount = 0;

        const checkStatus = async () => {
            const res = await fetch(`${url}/match/${matchId}/parse`);
            const result = await res.json();
            if (result.status !== "queued") {
                navigate(-1);
            }
        };

        const loadAnimation = async () => {
            setDisplay(<p className="MidText">{`Parse in progress${".".repeat(waitCount % 4)}`}</p>);
            waitCount++
        };

        const statusTimer = setInterval(checkStatus, 1000);
        const loadTimer = setInterval(loadAnimation, 500);
        return () => { clearInterval(statusTimer); clearInterval(loadTimer); }
    }, [navigate, params]);

    return (
        <div className="Page">
            {display}
        </div>
    );
}

export default Parse;

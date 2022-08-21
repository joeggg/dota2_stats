import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { url } from './consts'


function Parse() {
    const [params, _] = useSearchParams();
    const [display, setDisplay] = useState(<div></div>)
    const matchId = params.get("id");
    let waitCount = 0

    const checkStatus = async () => {
        const res = await fetch(`${url}/match/${matchId}/parse`);
        const result = await res.json();
        if (result.status !== "queued") {
            history.back()
        }
    }

    const loadAnimation = async () => {
        setDisplay(<p className="MidText">{`Parse in progress${".".repeat(waitCount % 4)}`}</p>);
        waitCount++
    }

    useEffect(() => {
        const statusTimer = setInterval(checkStatus, 1000);
        const loadTimer = setInterval(loadAnimation, 500);
        return () => { clearInterval(statusTimer); clearInterval(loadTimer); }
    }, []);

    return (
        <div className="Page">
            {display}
        </div>
    );
}

export default Parse;

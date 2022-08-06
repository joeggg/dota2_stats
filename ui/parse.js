import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { url } from './consts'


function Parse() {
    const [params, _] = useSearchParams();
    const [display, setDisplay] = useState(<div></div>)
    const matchId = params.get("id");

    const checkStatus = async () => {
        const res = await fetch(`${url}/match/${matchId}/parse`);
        const result = await res.json();
        console.log(result.status)
        if (result.status === "queued") {
            return setDisplay(<p>   Parse in progress</p>);
        }
        history.back()
    }

    useEffect(() => {
        const timer = setInterval(checkStatus, 1000);
        return () => clearInterval(timer)
    }, []);

    return (
        <div className="Page">
            {display}
        </div>
    );
}

export default Parse;

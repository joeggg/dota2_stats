import * as React from 'react'
import { Link } from 'react-router-dom';

function Main() {
    const idList = {
        Joe: 54269634,
        Nick: 14610489,
        Adam: 85245458,
        Alexi: 102949470,
    };
    const links = Object.entries(idList).map(([name, id]) => {
        return (
            <h2 key={id} className="Link">
                <Link to={`players/${id}`}>
                    {name}
                    <br />
                </Link>
            </h2>
        );
    });
    return <div className="Page">{links}</div>;
}

export default Main;

import React from 'react';
import { Link } from 'react-router-dom';

export default function Stats() {

    return (
        <>
        <div>
            <h1>Stats Page</h1>
            <table>
                <th>Stats Rolled</th>
                <tr>
                    <td>Strength</td>
                    <td>Agility</td>
                    <td>Wisdom</td>
                    <td>Constitution</td>
                    <td>Intelligence</td>
                    <td>Dexterity</td>
                </tr>
                <tr>
                    <td>15</td>
                    <td>15</td>
                    <td>15</td>
                    <td>15</td>
                    <td>15</td>
                    <td>15</td>
                </tr>
            </table>
            <button>Roll your stats</button>
        </div>
        <Link to='/'><button>Home Page</button></Link>
        <Link to='/classandequipment'><button>Next</button></Link>
        </>
    )
    }
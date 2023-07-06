import React from 'react';
import { Link } from 'react-router-dom';
import image from '../Components/image.png'

export default function OldCharacter() {

    return(
        <>
        <div>
            <h1>Jo Berg</h1>
            <table>
                <tr>
                    <td>Name</td>
                    <td>Appearance</td>
                    <td>Class</td>
                    <td>Equipment</td>
                    <td>Stats</td>
                </tr>
                <tr>
                    <td>Jo Berg</td>
                    <td><img src={image} alt={Image}/></td>
                    <td>Rogue</td>
                    <td>Dagger, Horse
                        <br></br>
                        Light Armor, Long Journey Rations
                        <br></br>
                        Small BackPack
                    </td>
                    <td>15, 15, 15
                        <br></br>
                        15, 15, 15
                    </td>
                </tr>
            </table>
        </div>
        <Link to='/savedcharacterspage'><button>Back</button></Link>
        <Link to='/'><button>Home Page</button></Link>
        </>
    )
}
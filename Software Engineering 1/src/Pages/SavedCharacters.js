import React from 'react';
import { Link } from 'react-router-dom';
import image from '../Components/image.png'

export default function SavedCharactersPage() {

    return (
        <>
        <div>
            <h1>Saved Characters Page</h1>
            <br></br>
            <table>
                <tr>
                    <td>Name</td>
                    <td>Class</td>
                    <td>Appearance</td>
                    <td>Delete</td>
                    <td>Advanced</td>
                </tr>
                <tr>
                    <td>Jo Berg</td>
                    <td>Rogue</td>
                    <td><img src={image} alt={Image}/></td>
                    <td><button>X</button> </td>
                    <td><Link to="/oldcharacter"><button>See</button></Link></td>
                </tr>
            </table>
        </div>
        <Link to='/'><button>Home Page</button></Link>
        </>
    )
    }
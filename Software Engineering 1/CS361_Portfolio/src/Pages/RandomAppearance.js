import React from 'react';
import { Link } from 'react-router-dom';
import image from '../Components/image.png'

export default function RandomAppearance() {

    return (
        <>
        <div>
            <h1>Random Appearance Page</h1>
        <img src={image} alt={Image}/>
        <br></br>
        <form>
        Name your character: <input type="text" name="charname"></input>
            <button>Done</button>
        </form>
        </div>
        <button>Redo?</button>
        <Link to='/'><button>Home Page</button></Link>
        <Link to='/stats'><button>Next</button></Link>
        </>
    )
    }
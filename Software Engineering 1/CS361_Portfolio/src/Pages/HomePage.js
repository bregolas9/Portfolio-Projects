import React from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {


  return (
    <>
      <h1>RPG Character Creator</h1>

      <Link to='/randomappearance'><button>Random Appearance Page</button></Link>
      <Link to='/stats'><button>Stats Page</button></Link>
      <Link to='/classandequipment'><button>Class and Equipment</button></Link>
      <Link to='/savedcharacterspage'><button>Saved Characters</button></Link>
    </>
  )
}

import React from 'react';
import { Link } from 'react-router-dom';

export default function ClassAndEquipment() {

    return (
        <>
        <div>
            <h1>Class and Equipment Page</h1>
            <h1>Select a Class</h1>

            <select>
                <option value="Rogue">Rogue</option>
                <option value="Knight">Knight</option>
                <option value="Archer">Archer</option>
                <option value="Priest">Priest</option>
                <option value="Wizard">Wizard</option>
            </select>

            <table>
                Equipment Selections
                <tr>
                    <td>Weapon Type</td>
                    <td>Armor Type</td>
                    <td>Backpack Type</td>
                    <td>Ration Type</td>
                    <td>Mount Type</td>
                </tr>
                <tr>
                    <td> Choose Weapon Type
                        <select>
                            <option value="Sword">Sword</option>
                            <option value="Bow">Bow</option>
                            <option value="Wand">Wand</option>
                            <option value="Staff">Staff</option>
                            <option value="Dagger">Dagger</option>
                        </select>
                    </td>
                    <td>Choose Armor Type
                        <select>
                            <option value="Heavy">Heavy</option>
                            <option value="Light">Light</option>
                            <option value="Medium">Medium</option>
                        </select>
                    </td>
                    <td>Choose Backpack Type
                        <select>
                            <option value="Large-Weighs 50lbs">Large-Weighs 50lbs</option>
                            <option value="Medium-Weighs 35lbs">Medium-Weighs 35lbs</option>
                            <option value="Small-Weighs 15lbs">Small-Weighs 15lbs</option>
                        </select>
                    </td>
                    <td>Choose Ration Type
                        <select>
                            <option value="Long Journey">Long Journey</option>
                            <option value="Short Journey">Short Journey</option>
                            <option value="Average Journey">Average Journey</option>
                        </select>
                    </td>
                    <td>Choose Mount Type
                        <select>
                            <option value="Horse">Horse</option>
                            <option value="Dragon">Dragon</option>
                            <option value="Cart">Cart</option>
                            <option value="None">None</option>
                        </select>
                    </td>
                </tr>
            </table>

        </div>
        <Link to='/'><button>Home Page</button></Link>
        <Link to='/savedcharacterspage'><button>Next</button></Link>
        </>
    )
}
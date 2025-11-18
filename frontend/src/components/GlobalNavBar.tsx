import { Link } from 'react-router-dom';
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from "../components/ui/navigation-menu"

// Consume the Context in Components
import { useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { GlobalModalDialogContext } from '../context/GlobalModalDialogContext';

function GlobalNavBar() {
    const user = useContext(UserContext);
    const signInDialog = useContext(GlobalModalDialogContext);

  return (
    <NavigationMenu>
    <NavigationMenuList>
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/">MarketWatch</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/tickers">Tickers</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/admin">Admin</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>

        {user ? <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/me">My Account</Link>
        </NavigationMenuLink>
        </NavigationMenuItem> : <NavigationMenuItem onClick={()=>signInDialog?.openDialog()}>
            Log In
        </NavigationMenuItem>}
    </NavigationMenuList>
    </NavigationMenu>
  );
}

export default GlobalNavBar;
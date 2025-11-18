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

import { useLocation } from 'react-router-dom';

function GlobalNavBar() {
  const location = useLocation();

    const currentUser = useContext(UserContext);
    const signInDialog = useContext(GlobalModalDialogContext);

  return (
    <NavigationMenu>
    <NavigationMenuList>
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/" className="text-primary-foreground">MarketWatch</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/tickers" className="text-primary-foreground">Tickers</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/admin" className="text-primary-foreground">Admin</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>

        {currentUser?.user ? (
        <NavigationMenuItem>
        <NavigationMenuLink asChild>
            <Link to="/me" className="text-primary-foreground">My Account</Link>
        </NavigationMenuLink>
        </NavigationMenuItem>) : (
        
        !location.pathname.includes('/admin') ? (
        <NavigationMenuItem onClick={()=>signInDialog?.openDialog()}>
            <NavigationMenuLink>
                Log In
            </NavigationMenuLink>
        </NavigationMenuItem>
        ) : (undefined)
    )}
    </NavigationMenuList>
    </NavigationMenu>
  );
}

export default GlobalNavBar;
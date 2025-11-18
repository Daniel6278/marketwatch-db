import { Link, useLocation } from "react-router-dom";
import { useContext } from "react";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "../components/ui/navigation-menu";
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu";
import { UserContext } from "../context/UserContext";
import { GlobalModalDialogContext } from "../context/GlobalModalDialogContext";

function GlobalNavBar() {
  const location = useLocation();
  const currentUser = useContext(UserContext);
  const signInDialog = useContext(GlobalModalDialogContext);

  return (
    <NavigationMenu>
      <NavigationMenuList>
        {/* MarketWatch */}
        <NavigationMenuItem>
          <NavigationMenuLink asChild>
            <Link
              to="/"
              className={navigationMenuTriggerStyle({ className: "!text-foreground" })}
            >
              MarketWatch
            </Link>
          </NavigationMenuLink>
        </NavigationMenuItem>

        {/* Tickers */}
        <NavigationMenuItem>
          <NavigationMenuLink asChild>
            <Link
              to="/tickers"
              className={navigationMenuTriggerStyle({ className: "!text-foreground" })}
            >
              Tickers
            </Link>
          </NavigationMenuLink>
        </NavigationMenuItem>

        {/* Admin */}
        <NavigationMenuItem>
          <NavigationMenuLink asChild>
            <Link
              to="/admin"
              className={navigationMenuTriggerStyle({ className: "!text-foreground" })}
            >
              Admin
            </Link>
          </NavigationMenuLink>
        </NavigationMenuItem>

        {/* User-specific links */}
        {currentUser?.user ? (
          <NavigationMenuItem>
            <NavigationMenuLink asChild>
              <Link
                to="/me"
                className={navigationMenuTriggerStyle({ className: "text-foreground" })}
              >
                My Account
              </Link>
            </NavigationMenuLink>
          </NavigationMenuItem>
        ) : (
          !location.pathname.includes("/admin") && (
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <button
                  type="button"
                  className={navigationMenuTriggerStyle({ className: "text-foreground" })}
                  onClick={() => signInDialog?.openDialog()}
                >
                  Log In
                </button>
              </NavigationMenuLink>
            </NavigationMenuItem>
          )
        )}
      </NavigationMenuList>
    </NavigationMenu>
  );
}

export default GlobalNavBar;

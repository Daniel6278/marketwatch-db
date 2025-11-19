import { Link, useLocation } from "react-router-dom";
import { useContext } from "react";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "../components/ui/navigation-menu";
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu";
import { UserContext } from "../context/ActiveUserContext";
import { useSignInDialog } from "../context/GlobalModalDialogsStatesContext";

function NavItem({
  to,
  children,
  className,
}: {
  to: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <NavigationMenuItem>
      <NavigationMenuLink asChild>
        <Link to={to} className={navigationMenuTriggerStyle({ className })}>
          {children}
        </Link>
      </NavigationMenuLink>
    </NavigationMenuItem>
  );
}

export default function GlobalNavBar() {
  const location = useLocation();
  const currentUser = useContext(UserContext);
  const signInDialog = useSignInDialog();

  const user = currentUser?.user;

  const baseLinks = [
    { to: "/", label: "MarketWatch", bold: true },
    { to: "/tickers", label: "Tickers" },
    { to: "/admin", label: "Admin" },
  ];

  const shouldShowLogin = !user && !location.pathname.includes("/admin");

  return (
    <>
      <NavigationMenu>
        <NavigationMenuList>
          {/* Core navigation links */}
          {baseLinks.map(({ to, label, bold }) => (
            <NavItem
              key={to}
              to={to}
              className={
                "cursor-pointer !text-foreground " + (bold ? "!font-bold" : "")
              }
            >
              {label}
            </NavItem>
          ))}

          {/* User-specific items */}
          {user
            ? !user.isAdmin() && <NavItem to="/me">My Account</NavItem>
            : shouldShowLogin && (
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <button
                      type="button"
                      className={navigationMenuTriggerStyle({
                        className: "!text-foreground",
                      })}
                      onClick={() => signInDialog?.openDialog()}
                    >
                      Log In
                    </button>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              )}
        </NavigationMenuList>
      </NavigationMenu>

      {user && (
        <div className="float-right rounded grid grid-rows-2 cursor-pointer">
          <span>Signed in as:</span>
          <em>{user?.displayName}</em>
        </div>
      )}

      <hr className="mt-3 mb-5" />
    </>
  );
}

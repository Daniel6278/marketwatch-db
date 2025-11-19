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
import {
  useSignInDialog,
  useSignOutDialog,
} from "../context/GlobalModalDialogsStatesContext";

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
  const { user } = useContext(UserContext) || {};
  const location = useLocation();
  const signInDialog = useSignInDialog();
  const signOutDialog = useSignOutDialog();

  function askUserSignOut() {
    signOutDialog.openDialog();
  }

  // --- Build links based on user role ---
  const links = [
    { to: "/", label: "MarketWatch", bold: true },
    { to: "/tickers", label: "Tickers" },
    ...(user?.isAdmin() || !user ? [{ to: "/admin", label: "Admin" }] : []),
  ];

  const shouldShowLogin = !user && !location.pathname.includes("/admin");

  return (
    <>
      {/* Signed-in identity display */}
      {user && (
        <div
          className="float-right rounded grid grid-rows-2 cursor-pointer bg-yellow-50"
          onClick={askUserSignOut}
        >
          <span>Signed in as:</span>
          <strong>{user.displayName}</strong>
        </div>
      )}

      <NavigationMenu>
        <NavigationMenuList>
          {/* Main links */}
          {links.map(({ to, label, bold }) => (
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

          {/* User-specific actions */}
          {user ? (
            <NavItem to="/me">My Account</NavItem>
          ) : (
            shouldShowLogin && (
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
            )
          )}
        </NavigationMenuList>
      </NavigationMenu>

      <hr className="mt-3 mb-5" />
    </>
  );
}

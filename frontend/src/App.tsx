import './App.css'; // Import the CSS file

import { Routes, Route } from 'react-router-dom';

import CreateAccount from './pages/CreateAccount';
import MyAccount from './pages/MyAccount';
import PriceHistory from './pages/PriceHistory';
import Tickers from './pages/Tickers';
import AdminDashboard from './pages/admin/Dashboard';
import Landing from './pages/Landing';
import GlobalNavBar from './components/GlobalNavBar';

export const API_ORIGIN = "https://specific-brande-data-group-585a3e34.koyeb.app";

import { Button } from "./components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card"
import SignIn from './components/SignIn';

import { useContext } from 'react';
import { GlobalModalDialogContext } from './context/GlobalModalDialogContext';
import { UserContext, UserIdentifier } from './context/UserContext';

function App() {
  const currentUser = useContext(UserContext);
  const signInDialog = useContext(GlobalModalDialogContext);

  async function login(email: string, password: string) {
    try {
        const response = await fetch(API_ORIGIN + '/signin', {
          method: "POST",
          body: JSON.stringify({
            email,
            password,
          }),
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const {id, credentials} = await response.json();
        currentUser?.setUser(new UserIdentifier(id, credentials));
    } catch (error) {
        console.error('Error logging in:', error);
    }
  }

  return (
    <>
    <div>
    <GlobalNavBar/>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/register" element={<CreateAccount />} />
      <Route path="/me" element={<MyAccount />} />
      <Route path="/pricehistory/:tickerSymbol" element={<PriceHistory />} />
      <Route path="/tickers" element={<Tickers />} />
      <Route path="/admin" element={<AdminDashboard />} />
    </Routes>
    </div>

    {(()=>{if (signInDialog?.dialogState.isOpen) {
      console.log("App.tsx : Dialog Is Open");
      return (<div className='fixed inset-0 z-[100] flex items-center justify-center' style={{backgroundColor:'#0008'}}>
        <Card>
        <CardHeader>
          <Button type="button" variant="secondary" onClick={()=>signInDialog.closeDialog()}>
            Close
          </Button>
        </CardHeader>
        <CardContent>
          <SignIn onLogin={login}/>
        </CardContent>
      </Card>
      </div>);
    }
    return undefined;
    })()}
    </>
  );
}

export default App;
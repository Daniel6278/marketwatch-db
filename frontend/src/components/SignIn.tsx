import React, { useState } from "react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Link } from "react-router-dom";

interface LoginProps {
  onLogin?: (email: string, password: string) => void;
}

const SignIn: React.FC<LoginProps> = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onLogin) onLogin(email, password);
  };

  return (
    <div>
    <h2>Sign In</h2>
    <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-1">
            <label className="text-sm font-medium">Email</label>
            <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            />
        </div>

        <div className="space-y-1">
            <label className="text-sm font-medium">Password</label>
            <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            />
        </div>

        <Button type="submit" className="w-full rounded-xl">
            Go
        </Button>
    </form>
    <hr/>
    <h3>Don’t have an account?</h3>
    <div>
        <Button asChild>
            <Link to='/register'>Create Your Account</Link>
        </Button>
    </div>
    </div>
  );
};

export default SignIn;

import React from "react";
import { useForm, Controller } from "react-hook-form";
import { Link } from "react-router-dom";

import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";

interface SignOutConfirmProps {
  onAction?: () => void;
}

const SignOutConfirm: React.FC<SignOutConfirmProps> = ({ onAction }) => {
  const handleLogOut = () => {
    onAction();
  };

  return (
    <div className="min-w-[400px]">
      <h2 className="mb-5 font-bold">Sign Out</h2>

      <p>Are you sure you want to sign out?</p>

      <Button
        type="button"
        className="w-full"
        variant="default"
        onClick={handleLogOut}
      >
        Sign Out
      </Button>
    </div>
  );
};

export default SignOutConfirm;

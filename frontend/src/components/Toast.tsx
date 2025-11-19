import { Button } from "./ui/button";

function Toast({
  message,
  variant,
  onOpenDetails,
}: {
  message: string;
  variant: "SUCCESS" | "FAIL";
  onOpenDetails: Function;
}) {
  return (
    <div className={`rounded p-4 ${variant == "FAIL" ? "bg-red" : "bg-green"}`}>
      <div className="grid grid-cols-[1fr_auto] gap-5">
        <span
          className="font-medium text-foreground line-clamp-2"
          style={{ fontSize: "75%" }}
        >
          {message}
        </span>
        <Button type="button" onClick={() => onOpenDetails()}>
          Dev Details
        </Button>
      </div>
    </div>
  );
}

export default Toast;

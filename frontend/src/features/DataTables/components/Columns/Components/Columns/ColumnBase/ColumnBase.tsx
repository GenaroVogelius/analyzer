import type { Column } from "@tanstack/react-table";
import { ArrowDown, ArrowUp, ChevronsUpDown } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

interface ColumnBaseProps<TData, TValue>
  extends React.HTMLAttributes<HTMLDivElement> {
  column: Column<TData, TValue>;
  title: string;
  children: React.ReactNode;
  tooltipContent?: string;
}

export function ColumnBase<TData, TValue>({
  column,
  title,
  className,
  children,
  tooltipContent,
}: ColumnBaseProps<TData, TValue>) {
  if (!column.getCanSort()) {
    return <div className={cn(className)}>{title}</div>;
  }

  const button = (
    <Button
      variant="ghost"
      size="sm"
      className="data-[state=open]:bg-accent -ml-3 h-8"
    >
      <span>{title}</span>
      {column.getIsSorted() === "desc" ? (
        <ArrowDown />
      ) : column.getIsSorted() === "asc" ? (
        <ArrowUp />
      ) : (
        <ChevronsUpDown />
      )}
    </Button>
  );

  const dropdown = (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        {tooltipContent ? (
          <TooltipTrigger asChild>{button}</TooltipTrigger>
        ) : (
          button
        )}
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start">{children}</DropdownMenuContent>
    </DropdownMenu>
  );

  return (
    <div className={cn("flex items-center gap-2", className)}>
      {tooltipContent ? (
        <Tooltip>
          {dropdown}
          <TooltipContent>
            <p>{tooltipContent}</p>
          </TooltipContent>
        </Tooltip>
      ) : (
        dropdown
      )}
    </div>
  );
}

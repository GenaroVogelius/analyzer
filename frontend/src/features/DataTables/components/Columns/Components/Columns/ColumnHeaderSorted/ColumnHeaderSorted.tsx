import type { Column } from "@tanstack/react-table";
import { ArrowDown, ArrowUp, EyeOff } from "lucide-react";
import { ColumnBase } from "../ColumnBase/ColumnBase";

import {
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";

interface ColumnHeaderProps<TData, TValue>
  extends React.HTMLAttributes<HTMLDivElement> {
  column: Column<TData, TValue>;
  title: string;
  tooltipContent?: string;
}

export function ColumnHeaderSorted<TData, TValue>({
  column,
  title,
  className,
  tooltipContent,
}: ColumnHeaderProps<TData, TValue>) {
  if (!column.getCanSort()) {
    return <div className={cn(className)}>{title}</div>;
  }

  return (
    <ColumnBase
      column={column}
      title={title}
      className={className}
      tooltipContent={tooltipContent}
    >
      <DropdownMenuItem onClick={() => column.clearSorting()}>
        By Default
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem onClick={() => column.toggleSorting(false)}>
        <ArrowUp />
        Ascendent
      </DropdownMenuItem>
      <DropdownMenuItem onClick={() => column.toggleSorting(true)}>
        <ArrowDown />
        Descendent
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem onClick={() => column.toggleVisibility(false)}>
        <EyeOff />
        Hide Column
      </DropdownMenuItem>
    </ColumnBase>
  );
}

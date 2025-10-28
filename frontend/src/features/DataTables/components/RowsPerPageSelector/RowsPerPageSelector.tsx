import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { TableState } from "@tanstack/react-table";

export interface RowsPerPageSelectorProps {
  tableState: TableState;
  setPageSize: (pageSize: number) => void;
}

export function RowsPerPageSelector({
  tableState,
  setPageSize,
}: RowsPerPageSelectorProps) {
  return (
    <div className="hidden items-center gap-2 lg:flex">
      <Label htmlFor="rows-per-page" className="text-sm font-medium">
        Filas por página
      </Label>
      <Select
        value={`${tableState.pagination.pageSize}`}
        onValueChange={(value) => {
          setPageSize(Number(value));
        }}
      >
        <SelectTrigger size="sm" className="w-20" id="rows-per-page">
          <SelectValue placeholder={tableState.pagination.pageSize} />
        </SelectTrigger>
        <SelectContent side="top">
          {[10, 20, 30, 40, 50].map((pageSize) => (
            <SelectItem key={pageSize} value={`${pageSize}`}>
              {pageSize}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

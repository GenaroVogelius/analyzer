import { Checkbox } from "@/components/ui/checkbox";
import { createColumnHelper } from "@tanstack/react-table";
import { ColumnHeaderSorted } from "../../../components/Columns/Components/Columns/ColumnHeaderSorted/ColumnHeaderSorted";
import { DragHandler } from "../../../components/Columns/Components/DragHandler/DragHandler";

export type PositionsColumnsType = {
  id: number;
  type_operation: string;
  ticket: string;
  species: string;
  reference: string;
  amount: number;
  code: string;
  accumulated: number;
  number_receipt: number;
  date_liquidation: string;
  date_operation: string;
};

const columnHelper = createColumnHelper<PositionsColumnsType>();

export const PositionsColumns = [
  columnHelper.display({
    id: "drag",
    header: () => null,
    cell: ({ row }) => <DragHandler id={row.original.id} />,
  }),
  columnHelper.display({
    id: "select",
    header: ({ table }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={
            table.getIsAllPageRowsSelected() ||
            (table.getIsSomePageRowsSelected() && "indeterminate")
          }
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Select all"
        />
      </div>
    ),
    cell: ({ row }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Select row"
        />
      </div>
    ),
    enableSorting: false,
    enableHiding: false,
  }),
  columnHelper.accessor("ticket", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Ticket" tooltipContent="Ticket" />
    ),
    cell: ({ getValue }) => {
      return <span>{getValue()}</span>;
    },
  }),
  columnHelper.accessor("type_operation", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Type Operation" tooltipContent="Type Operation" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("species", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Species" tooltipContent="Species" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("amount", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Amount" tooltipContent="Amount" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("date_operation", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Date Operation"
        tooltipContent="Profit and losses promedio nominal"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "datetime",
  }),
  columnHelper.accessor("date_liquidation", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Date Liquidation"
        tooltipContent="Date liquidation"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "datetime",
  }),

  // columnHelper.accessor("importe_promedio", {
  //   header: ({ column }) => <ColumnHeader column={column} title="Importe" />,
  //   cell: ({ row, getValue }) => (
  //     <form
  //       onSubmit={(e) => {
  //         e.preventDefault();
  //         toast.promise(new Promise((resolve) => setTimeout(resolve, 1000)), {
  //           loading: `Saving ${row.original.TNA_promedio}`,
  //           success: "Done",
  //           error: "Error",
  //         });
  //       }}
  //     >
  //       <Label htmlFor={`${row.original.id}-limit`} className="sr-only">
  //         Limit
  //       </Label>
  //       <Input
  //         className="hover:bg-input/30 focus-visible:bg-background dark:hover:bg-input/30 dark:focus-visible:bg-input/30 h-8 w-16 border-transparent bg-transparent text-right shadow-none focus-visible:border dark:bg-transparent"
  //         defaultValue={getValue()}
  //         id={`${row.original.id}-limit`}
  //       />
  //     </form>
  //   ),
  //   sortingFn: "basic",
  // }),

  // columnHelper.display({
  //   id: "actions",
  //   cell: () => (
  //     <DropdownMenu>
  //       <DropdownMenuTrigger asChild>
  //         <Button
  //           variant="ghost"
  //           className="data-[state=open]:bg-muted text-muted-foreground flex size-8"
  //           size="icon"
  //         >
  //           <Ellipsis />
  //           <span className="sr-only">Open menu</span>
  //         </Button>
  //       </DropdownMenuTrigger>
  //       <DropdownMenuContent align="end" className="w-32">
  //         <DropdownMenuItem>Edit</DropdownMenuItem>
  //         <DropdownMenuItem>Make a copy</DropdownMenuItem>
  //         <DropdownMenuItem>Favorite</DropdownMenuItem>
  //         <DropdownMenuSeparator />
  //         <DropdownMenuItem variant="destructive">Delete</DropdownMenuItem>
  //       </DropdownMenuContent>
  //     </DropdownMenu>
  //   ),
  // }),
];

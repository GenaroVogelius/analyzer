import { Header } from "@/components/Header";
import { SectionsTabs } from "@/components/SectionsTabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent } from "@/components/ui/tabs";
import { OperationsDashboard } from "@/features/OperationsDashboard";
import { ClosedPositionsDashboard } from "@/features/ClosedPositionsDashboard";
import React from "react";

export const MainDashboard: React.FC = () => {

  class Enum {
    static readonly Operations = "operations";
    static readonly ClosedPositions = "closedPositions";
  }

  const sections = [
    { value: Enum.Operations, title: "📋 Your operations" },
    { value: Enum.ClosedPositions, title: "📊 Your closed positions"},
  ];

  const tabsContent = [
    {
      value: Enum.Operations,
      component: (
        <Card>
          <CardHeader>
            <CardTitle className="text-center">Your operations table view</CardTitle>
            <CardDescription className="text-center">
              See all your operations in a table view
            </CardDescription>
          </CardHeader>
          <CardContent>
          <OperationsDashboard />,
          </CardContent>
        </Card>
      ),
    },
    {
      value: Enum.ClosedPositions,
      component: (
        <Card>
          <CardHeader>
            <CardTitle className="text-center">Your closed positions</CardTitle>
            <CardDescription className="text-center">
              See all your closed positions in a table view
            </CardDescription>
          </CardHeader>
          <CardContent>
          <ClosedPositionsDashboard />,
          </CardContent>
        </Card>
      ),
    },

  ];
  return (
    <div className="p-4 min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue={Enum.Operations} className="space-y-6">
          <SectionsTabs sections={sections} />
          {tabsContent.map((tab) => (
            <TabsContent key={tab.value} value={tab.value}>
              {tab.component}
            </TabsContent>
          ))}
        </Tabs>
      </main>
    </div>
  );
};

import { Button } from "@/app/components/ui/button";
import { useBotStore } from "@/app/store/bot";
import { Undo2 } from "lucide-react";
import Locale from "@/app/locales";
import { useMobileScreen } from "../../utils/mobile";
import { useSidebarContext } from "@/app/components/home";
import { Separator } from "../ui/separator";
import Typography from "../ui/typography";

export default function ChatHeader() {
  const isMobileScreen = useMobileScreen();
  const { setShowSidebar } = useSidebarContext();
  const botStore = useBotStore();
  const bot = botStore.currentBot();
  const session = botStore.currentSession();
  const numberOfMessages =
    (bot.botHello?.length ? 1 : 0) + session.messages.length;
  return (
    <div className="relative">
      <div className="absolute top-4 left-5">
        {isMobileScreen && (
          <Button
            size="mini"
            variant="outline"
            title={Locale.Chat.Actions.ChatList}
            onClick={() => setShowSidebar(true)}
          >
            <Undo2 />
          </Button>
        )}
      </div>
      <div className="text-center py-1">
        <Typography.H4>{bot.name}</Typography.H4>
        <div className="text-sm text-muted-foreground">
          {Locale.Chat.SubTitle(numberOfMessages)}
        </div>
      </div>
      <Separator />
    </div>
  );
}

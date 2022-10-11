package main

import (
	"context"
	"flag"
	"log"

	"github.com/kenshaw/evdev"
)

func main() {
	flag.Parse()
	evt, evt_err := evdev.OpenFile("/dev/input/event4")
	if evt_err != nil {
		log.Fatal(evt_err)
	}
	defer evt.Close()

	eventCh := evt.Poll(context.Background())

	for event := range eventCh {
		if event == nil {
			break
		}
		switch typ := event.Type.(type) {
		case evdev.KeyType:
			if typ == evdev.KeyQ {
				log.Printf("quitting")
				break
			}
		case evdev.AbsoluteType:
			log.Printf("recieved absolute axis event: %+v", event)
			log.Printf("	axis info: %+v", evt.AbsoluteTypes())
		}
	}
}

TaskHandle_t Task1;

void Task1code( void * parameter) {
  for(;;) {
    Serial.print("Task1: loop() running on core ");
    Serial.println(xPortGetCoreID());
    delay(1000);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.print("setup() running on core ");
  Serial.println(xPortGetCoreID());
  xTaskCreatePinnedToCore(
      Task1code, /* Function to implement the task */
      "Task1", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      1,  /* Priority of the task */
      &Task1,  /* Task handle. */
      0); /* Core where the task should run */
}

void loop() {
  Serial.print("Main: loop() running on core ");
  Serial.println(xPortGetCoreID());
  Serial.print("Main: Wait for 10s ...");
  delay(10000);
  Serial.print("Main: Delete Task 1");
  vTaskDelete(Task1);
}
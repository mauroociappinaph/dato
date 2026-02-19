import { Controller, Get, Module } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';

@Controller()
class AppController {
  @Get()
  getHello(): { message: string } {
    return { message: 'DATO API' };
  }
}

@Module({
  controllers: [AppController],
})
class AppModule {}

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);
  await app.listen(3001);
}

void bootstrap();

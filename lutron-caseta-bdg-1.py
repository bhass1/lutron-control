import asyncio, random, telnetlib3, time
from time import sleep

"""Script made for Halloween 2022 to simulate a ghost encounter by randomly flickering lights

Copyright (c) 2022 Bill Hass

This work is licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or
send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""


class CasetaLight:
  """Factory to piece together telnet strings for light control"""
  _id = None # Integration ID
  _fade_time = 0.0
  _delay_time = 0.0

  def __init__(self, integration_id):
    self._id = integration_id 

  def set_output_level(self, output_level):
    command = (f'#OUTPUT,{self._id},1,{output_level}'
      f',{self._fade_time},{self._delay_time}\n')
    print(f'{command}')
    return command

  def get_output_level(self):
    command = (f'?OUTPUT,{self._id},1\n')
    print(f'{command}')
    return command

  def turn_on(self):
    return self.set_output_level(100.00)

  def turn_off(self):
    return self.set_output_level(0.00)


async def ghost_sequence(writer, writer_lock, caseta_light):
  """Flicker lights randomly to simulate a ghost encounter"""
  for i in range(0, random.randrange(6, 16)):
    async with writer_lock:
      writer.write(caseta_light.turn_off())
    await asyncio.sleep(random.uniform(0.1, 0.5))
    async with writer_lock:
      writer.write(caseta_light.turn_on())
    await asyncio.sleep(random.uniform(0.1, 0.75))

# Finds id of device based on the only device with 100.00 OUTPUT
#async def find_id_on_light():
#    id_guess = 0
#    while True:
#        prompt = await reader.read(1024)
#        if not prompt:
#          print('input> EOF')
#          # End of File
#          break
#        elif 'login' in prompt:
#          print('input> login')
#          writer.write('lutron\n')
#        elif 'password' in prompt:
#          print('input> password')
#          writer.write('integration\n')
#        elif'~ERROR' in prompt:
#          #Bring the prompt back up to trigger the input parsing loop
#          id_guess += 1
#          writer.write('\n') 
#        elif '~OUTPUT' in prompt:
#          if id_guess:
#            current_output_level = prompt.split(',')[-1]
#            print(f'{id_guess} - {current_output_level}')
#            if current_output_level.strip() == '100.00':
#              print(f'The correct id is {id_guess}')
#          #Bring the prompt back up to trigger the input parsing loop
#          id_guess += 1
#          writer.write('\n') 
#          sleep(5)
#        elif 'GNET>' in prompt:
#          kitchen_light = CasetaLight(2)
#          test_light = CasetaLight(id_guess)
#          writer.write(test_light.get_output_level())
#
#        # display all server output 
#        print(prompt, flush=True)

async def shell(reader, writer):
    writer_lock = asyncio.Lock()
    while True:
        prompt = await reader.read(1024)
        if not prompt:
          print('input> EOF')
          # End of File
          break
        elif 'login' in prompt:
          print('input> login')
          writer.write('lutron\n')
        elif 'password' in prompt:
          print('input> password')
          writer.write('integration\n')
        elif'~ERROR' in prompt:
          #Bring the prompt back up to trigger the input parsing loop
          writer.write('\n') 
        elif '~OUTPUT' in prompt:
          #Bring the prompt back up to trigger the input parsing loop
          writer.write('\n') 
        elif 'GNET>' in prompt:
          kitchen_light = CasetaLight(2)
          wall_light = CasetaLight(5)
          await asyncio.gather( 
            ghost_sequence(writer, writer_lock, wall_light),
            ghost_sequence(writer, writer_lock, kitchen_light)
          )
          event_delay = random.randrange(5,25)
          print(f'{time.strftime("%X")} Next ghost event in {event_delay} minutes')
          sleep(event_delay*60)

        # display all server output 
        print(prompt, flush=True)

    # EOF
    print()

def main():
  loop = asyncio.get_event_loop()
  coro = telnetlib3.open_connection('192.168.169.207', 23, shell=shell)
  reader, writer = loop.run_until_complete(coro)
  loop.run_until_complete(writer.protocol.waiter_closed)

if __name__ == "__main__":
  main()

from distutils.core import setup
import py2exe

musicFiles = ['Music/Oblivion.mp3']

combatSoundFiles = ['Sounds/Combat/RevolverShot.mp3',
					'Sounds/Combat/CrossbowShot.mp3',
					'Sounds/Combat/EmptyGun.mp3',
					'Sounds/Combat/MeleeMiss.mp3',
					'Sounds/Combat/RevolverReload.mp3']

miscSoundFiles = ['Sounds/Misc/FootstepsHall.mp3',
				  'Sounds/Misc/GenericDoor1.mp3',
				  'Sounds/Misc/GenericDoor2.mp3',
				  'Sounds/Misc/HeavyDoor.mp3',
				  'Sounds/Misc/ItemGet.mp3',
				  'Sounds/Misc/KeyGet.mp3',
				  'Sounds/Misc/LiquorDrink.mp3',
				  'Sounds/Misc/LoudCrash.mp3',
				  'Sounds/Misc/PaperGet1.mp3',
				  'Sounds/Misc/PaperGet2.mp3',
				  'Sounds/Misc/PaperGet3.mp3']

monsterSoundFiles = ['Sounds/Monsters/BentHostLaugh.mp3',
					 'Sounds/Monsters/DemonCantWait.mp3',
					 'Sounds/Monsters/DemonLatin.mp3',
					 'Sounds/Monsters/DemonDeath.mp3',
					 'Sounds/Monsters/HellhoundDeath.mp3',
					 'Sounds/Monsters/HellhoundGrowl.mp3']

UISoundFiles = ['Sounds/UI/menuClick.mp3',
				'Sounds/UI/menuHover.wav']

spriteFiles = ['Sprites/buttonHighLight.png',
			   'Sprites/buttonNormal.png',
			   'Sprites/buttonPressed.png',
			   'Sprites/ekgOK.png',
			   'Sprites/ekgDANGER.png',
			   'Sprites/ekgCAUTION.png',
			   'Sprites/ekgCAUTION2.png']

setup (console=['__init__.py'],
data_files=[('Sounds/Combat',combatSoundFiles),
			('Sounds/Monsters',monsterSoundFiles),
			('Sounds/Misc',miscSoundFiles),
			('Sounds/UI',UISoundFiles),
			('Music', musicFiles), 
			('Sprites', spriteFiles)])
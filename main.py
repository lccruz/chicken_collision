# -*- coding:utf-8 -*-
import math
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *
from panda3d.core import Point3, Texture, TextureStage
from random import randint, choice, random, randrange, uniform

NUMERO_CUBOS = 8
SPEED_MIM = 0.02
SPEED_MAX = 0.09


def get_pos():

    lista_pos = [
        (0, 10.0, 0),
        (10.0, 0, 90),
        (0, -10.0, 180),
        (-10.0, 0, 270),
    ]
    return lista_pos[randrange(0, len(lista_pos))]


class Chicken(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.title = OnscreenText(text="Chicken Collision 3D",
                                  style=1, fg=(255, 255, 255, 1),
                                  pos=(0.8, -0.95), scale = .07)

        # seta cor de fundo
        self.setBackgroundColor(0.1, 0.0, 0.0)

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(255, 255, .255, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(0, 0, -2.5))
        directionalLight.setColor(Vec4(255, 255, 255, 1))
        self.render.setLight(self.render.attachNewNode(ambientLight))
        self.render.setLight(self.render.attachNewNode(directionalLight))

        # Cria o Traverser e handlers: primeiro passo para detectar colisao
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        base.pusher.addInPattern('%fn-into-%in')

        # ESFERA
        self.esfera = self.loader.loadModel("models/esfera")
        self.esfera.reparentTo(self.render)
        self.esfera.setScale(1, 1, 1)
        self.esfera.setPos(0, 0, 0)
        textureEsfera = self.loader.loadTexture("textures/logo_python.jpg")
        textureEsfera.setWrapU(Texture.WMRepeat)
        textureEsfera.setWrapV(Texture.WMRepeat)
        stageEsfera = TextureStage("Esfera")
        self.esfera.setTexture(stageEsfera, textureEsfera)

        # Cria colliders: segundo passo
        self.esferaCEsfera = CollisionNode("esferaCEsfera")
        self.esferaCEsfera.addSolid(CollisionSphere(0, 0, 0, 1))
        self.esferaEsfNP = self.esfera.attachNewNode(self.esferaCEsfera)
        self.esferaEsfNP.show()

        self.collision_names = NUMERO_CUBOS*'0'.split()
        self.cubos = NUMERO_CUBOS*'0'.split()
        self.criaCubos()

        # Adiciona uma função a lista de tasks
        self.gameTask = taskMgr.add(self.moveCubos, "move")

        for nome in self.collision_names:
            self.accept('%s-into-esferaCEsfera' % (nome), self.colideCentro)

    def criaCubos(self):

        for i in range(len(self.cubos)):
            self.criaCubo(i)

    def criaCubo(self, i):

        # CUBO
        # Load the environment model.
        cubo = self.loader.loadModel("models/chicken")
        # Reparent the model to render.
        cubo.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        x, y, direcao = get_pos()
        cubo.setScale(1, 1, 1)
        cubo.setPos(x, y, 0)
        cubo.setHpr(direcao, 0, 0)
        cubo.setTag("velocidade", str(uniform(SPEED_MIM, SPEED_MAX)))
        # Cria colliders
        collision_name = "cuboCEsfera%s" % (i)
        self.cuboCEsfera = CollisionNode(collision_name)
        self.cuboCEsfera.addSolid(CollisionSphere(0, 0, 0, 1))
        self.cuboEsfNP = cubo.attachNewNode(self.cuboCEsfera)
        # Apontar ao Traverser e ao Handler, quais objetos devem ser observados
        # ao colidir e como tratar as colisões entre eles : terceiro passo
        base.cTrav.addCollider(self.cuboEsfNP, base.pusher)
        base.pusher.addCollider(self.cuboEsfNP, cubo)
        self.collision_names[i] = collision_name
        self.cubos[i] = cubo

    def colideCentro(self, entrada):
        entrada_name = entrada.getFromNode().get_name()
        collision_name_pos = self.collision_names.index(entrada_name)
        self.cubos[collision_name_pos].remove()
        self.criaCubo(collision_name_pos)
        audio = "audios/%s.mp3" % (randrange(1, 16))
        mySound = base.loader.loadSfx(audio)
        mySound.play()
        print "colidiu"

    # Função responsavel por movimentar o cubo
    def updatePos(self, obj):

        if obj:
            direcao = obj.getHpr()[0]
            speed = float(obj.getTag("velocidade"))
            if direcao == 0.0:
                obj.setY(obj.getY()-speed)
            elif direcao == 90.0:
                obj.setX(obj.getX()-speed)
            elif direcao == 180.0:
                obj.setY(obj.getY()+speed)
            elif direcao == 270.0:
                obj.setX(obj.getX()+speed)
            else:
                print "erro"

    def moveCubos(self, task):

        # update cubos
        for obj in self.cubos:
            self.updatePos(obj)

        return Task.cont

app = Chicken()
app.run()

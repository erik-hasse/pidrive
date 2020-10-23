from concurrent import futures

import cv2
import grpc

from pidrive.hardware import PiCarV

import car_pb2
import car_pb2_grpc


class CarService(car_pb2_grpc.CarServicer):
    def __init__(self, car):
        self.car = car
        self.vid = cv2.VideoCapture(-1)

    def move(self, request, context):
        self.car.velocity = request.velocity
        self.car.angle = request.angle
        return car_pb2.MoveReply()

    def image(self, request, context):
        ret, frame = self.vid.read(-1)
        return car_pb2.ImageReply(
            image_array=frame.tobytes(),
            shape=frame.shape,
            dtype=frame.dtype.str
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    car_pb2_grpc.add_CarServicer_to_server(
        CarService(PiCarV()),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

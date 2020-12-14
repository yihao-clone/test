# Setup:
# create pipeline
pipe = rs.pipeline()
# create config object
cfg = rs.config()
# tell config that we will use recorded device from file
# to be used by the pipeline through playback
cfg.enable_device_from_file("../data/distance_test.bag")
#cfg.enable_all_streams()
align_to = rs.stream.infrared
align = rs.align(align_to)
# start streaming from file
profile = pipe.start(cfg)
# setup colorizer for depthmap
colorizer = rs.colorizer()

# setup playback
playback = profile.get_device().as_playback()
playback.set_real_time(False)
# get the duration of the video
t = playback.get_duration()
t.seconds
# compute the number of frames (30fps setting)
frame_counts = t.seconds * 30

# extract and save all depth frames
result = []
spec = 0
ir_frames = []
for i in range(frame_counts):
    #print(i)
    frame = pipe.wait_for_frames()
    #aligned = align.process(frame)
    ir = frame.get_infrared_frame()
    ir_frames.append(ir)
    depth = frame.get_depth_frame()
    #result.append(np.asanyarray(colorizer.colorize(depth).get_data()))
    #tmp = np.asanyarray(colorizer.colorize(depth).get_data())
    result.append(depth)
    #io.imsave("../outputs/distance_test/" + str(i) + ".jpg", tmp)
    #result.append(tmp)
    #if i == 16:
        #spec = np.asanyarray(colorizer.colorize(depth).get_data())
        #color = frame.get_color_frame()
playback.pause()
pipe.stop()

dt = pixel_distance(result[31], ir_frames[31], 384, 363, 708, 401)
print(dt)

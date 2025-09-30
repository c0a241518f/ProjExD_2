import os
import pygame as pg
import random
import sys
import time



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値:判定結果タプル（横方向, 縦方向）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向にはみ出ていたら
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None: #機能１
    """
    引数：スクリーンSurface
    戻り値：なし
    """
    bg_img = pg.Surface((WIDTH, HEIGHT)) 
    pg.draw.rect(bg_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT)) #黒い短形を描写
    bg_img.set_alpha(200) #黒い短形の透明度の設定
    fonto = pg.font.Font(None, 40)
    txt = fonto.render("Game Over", True, (255, 255, 255)) #白文字Gaem OverのSurface
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2
    bg_img.blit(txt, txt_rct)
    kk1_img = pg.image.load("fig/8.png") #泣いてるこうかとん画像のロード
    bg_img.blit(kk1_img, [350,280])
    bg_img.blit(kk1_img, [720,280])
    screen.blit(bg_img, [0, 0]) #スクリーンにゲームオーバー画面を描写
    pg.display.update()
    time.sleep(5) #５秒間表示

def init_bb_imgs() -> tuple[list[pg.Surface]]: #機能２
    """
    引数：なし
    戻り値：大きさを変えた爆弾のSurfaceリストと爆弾の加速度リスと
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]: #機能３
    """
    引数：なし
    戻り値：押下キーに対する移動量の合計値タプルをキー，rotozoomしたこうかとん画像のSurfaceを値とした辞書
    """
    kk_img = pg.image.load("fig/3.png")
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0), # キー押下がない場合
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 1.0), # 右
        (+5,-5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1.0), # 右上
        (0,-5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 1.0), # 上
        (-5,-5): pg.transform.rotozoom(kk_img, -45, 1.0), # 左上
        (-5,0): pg.transform.rotozoom(kk_img, 0, 1.0), # 左
        (-5,+5): pg.transform.rotozoom(kk_img, 45, 1.0), # 左下
        (0,+5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90, 1.0), # 下
        (+5,+5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1.0), # 右下
    }
    
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #赤い爆弾円
    bb_img.set_colorkey((0, 0, 0)) #四隅の黒い部分をなくす
    bb_rct = bb_img.get_rect() #爆弾rect
    bb_rct.centerx = random.randint(0, WIDTH) #爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT) #爆弾縦座標
    vx, vy = +5, +5 #爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs() # 機能２のリスト２つを所得
    kk_imgs = get_kk_imgs() #機能３の辞書取得

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            gameover(screen)
            return #ゲームオーバー
        
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量を加算
                sum_mv[1] += mv[1] #縦方向の移動量を加算
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx,avy) #爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみ出ていたら
            vx *= -1
        if not tate: #縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct) #爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
